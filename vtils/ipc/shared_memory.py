import numpy as np
from multiprocessing import shared_memory

HELP="""
Utility to quickly create on a shared memory array that can be accessed and edited by multiple programs::
To create a shared memory array:
  - Input: name of the shared memory to create and the initial values of the array
  - Output: shared_memory_array
To access a shared memory
  - Input: name, shape, and dtype of the shared memory to access
  - Output: shared_memory_array
"""
class shared_memory_array():
  def __init__(self, name:str, init_array:np.array=None, shape:np.shape=None, dtype:np.dtype=None):
    self.shm = None
    self.val = None

    if init_array is not None:
      assert shape is None and dtype is None, "Check input: \n"+HELP
      self.register_shared_memory(memory_name=name, memory_value=init_array)
    else:
      assert shape is not None and dtype is not None, "Check inputs: \n"+HELP
      self.access_shared_memory(memory_name=name, shape=shape, dtype=dtype)

  def register_shared_memory(self, memory_name, memory_value):
    shm = shared_memory.SharedMemory(create=True, size=memory_value.nbytes, name=memory_name)
    val_shared = np.ndarray(memory_value.shape, dtype=memory_value.dtype, buffer=shm.buf)
    val_shared[:] = memory_value[:]  # Copy the original data into shared memory
    self.shm = shm
    self.val = val_shared

  def access_shared_memory(self, memory_name, shape, dtype):
    existing_shm = shared_memory.SharedMemory(name=memory_name)
    val_shared = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
    self.shm = existing_shm
    self.val = val_shared

  def close_link(self):
    # Close access to the shared memory from this instance.
    self.shm.close()

  def delete_memory(self):
    # Request that the underlying shared memory block be destroyed. Call only once
    self.shm.unlink()

  @property
  def name(self):
    return self.shm.name

if __name__ == '__main__':
  print(HELP)
  user_data = np.array([1, 1, 2, 3, 5, 8.0])

  # share data on shared memory
  shared_user_data = shared_memory_array(name="shared_mem_name", init_array=user_data)

  # access data on shared memory
  access_user_data = shared_memory_array(name="shared_mem_name", shape=user_data.shape, dtype=user_data.dtype)

  # Check data
  print(f"Original user data: {user_data}")
  print(f"Data accessed over shared memory: {access_user_data.val}")

  # release shared memory link
  shared_user_data.close_link()
  access_user_data.close_link()

  # Request removal of shared memory. Only one process needs to call it
  shared_user_data.delete_memory()
