from multiprocessing import shared_memory

import numpy as np

HELP = """
------------------------------------------------------------------------
Utility to quickly create on a shared memory array that can be accessed
and edited by multiple programs::
Input:
    - name:         name of the shared memory to create
    - init_array :  initial values of the array
                    - used to create shared memory if one doesn't exists
                    - used to determine memory shape and dtype
Output: shared_memory_array
------------------------------------------------------------------------
"""


class shared_memory_array:
    def __init__(self, name: str, init_array: np.array):  # initial array values to use
        self.shm = None
        self.val = None

        if init_array is not None:
            shape = init_array.shape
            dtype = init_array.dtype

        try:
            self.access_shared_memory(memory_name=name, shape=shape, dtype=dtype)
            print(f"Vtils:> Shared memory ({name}) found.")
        except FileNotFoundError:
            if init_array is None:
                raise ValueError(
                    f"Vtils:> Shared memory ({name}) not found and no init_array provided."
                )
            else:
                print(
                    f"Vtils:> Shared memory ({name}) not found. Created a new shared memory using init_array"
                )
                self.register_shared_memory(memory_name=name, memory_value=init_array)

    def register_shared_memory(self, memory_name, memory_value):
        shm = shared_memory.SharedMemory(
            create=True, size=memory_value.nbytes, name=memory_name
        )
        val_shared = np.ndarray(
            memory_value.shape, dtype=memory_value.dtype, buffer=shm.buf
        )
        val_shared[:] = memory_value[:]  # Copy the original data into shared memory
        self.shm = shm
        self.val = val_shared

    def access_shared_memory(self, memory_name, shape, dtype):
        existing_shm = shared_memory.SharedMemory(name=memory_name)
        val_shared = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
        self.shm = existing_shm
        self.val = val_shared

    def close_link(self):
        if self.shm is not None:
            # Close access to the shared memory from this instance.
            self.shm.close()
            print(f"Vtils:> Shared memory ({self.name}) closed")

    def delete_memory(self):
        if self.shm is not None:
            # Request that the underlying shared memory block be destroyed. Call only once
            self.shm.unlink()
            print(f"Vtils:> Shared memory ({self.name}) deleted")
            self.shm = None

    @property
    def name(self):
        if self.shm is not None:
            return self.shm.name

    def __del__(self):
        self.close_link()


if __name__ == "__main__":
    print(HELP)
    user_data = np.array([1, 1, 2, 3, 5, 8.0])
    print(f"Original user data: {user_data}")

    # share data on shared memory
    shared_user_data = shared_memory_array(name="shared_mem_name", init_array=user_data)

    # access data on shared memory
    for i in range(3):
        access_user_data = shared_memory_array(
            name="shared_mem_name", init_array=user_data
        )

        # Check accessed data
        print(f"\t[Loop{i}]: Data accessed over shared memory: {access_user_data.val}")

        # release shared memory link
        shared_user_data.close_link()

    access_user_data.close_link()

    # Request removal of shared memory. Only one process needs to call it
    shared_user_data.delete_memory()
