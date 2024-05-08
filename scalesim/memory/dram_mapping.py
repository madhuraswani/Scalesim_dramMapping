import math
import numpy as np
from tqdm import tqdm

class dram_mapping:
    def __init__(self):
        self.num_banks=1
        self.num_lines_per_bank = 0
        self.type_of_Mapping="None"
        self.num_bankAccess={}
    def set_params(self,num_banks,type_of_mapping):
        self.num_banks=num_banks
        self.type_of_Mapping=type_of_mapping
        for i in range(num_banks):
            self.num_bankAccess[i]=[]

    def __call__(self, input) -> np.Any:
        mappings={
            "Normal": self.Normal_Mapping
        }
        submatrices=mappings[self.type_of_Mapping](input,self.num_banks)
        self.num_lines_per_bank=input.shape[0]//self.num_banks
        return submatrices
    
    """
    Define the mapping in this file and add the mapping to the call function. In the mappings dictionary.
    """

    def alternate_mapping(self,matrix):
        num_rows = matrix.shape[0]
        rows_per_submatrix = num_rows // self.num_banks
        remainder = num_rows % self.num_banks

        submatrices=[[] for _ in range(self.num_banks)]

        for j in rows_per_submatrix:
            pass

    def Normal_Mapping(self,matrix, num_Banks):
    # Get the number of rows in the matrix
        num_rows = matrix.shape[0]
    # Calculate the number of rows in each submatrix
        rows_per_submatrix = num_rows // num_Banks
        remainder = num_rows % num_Banks
        # Initialize an empty list to store the submatrices
        submatrices = []
        # Split the matrix into submatrices
        start_index = 0
        for i in range(num_Banks):
            if remainder > 0:
                end_index = start_index + rows_per_submatrix + 1
                remainder -= 1
            else:
                end_index = start_index + rows_per_submatrix
            # Extract the submatrix and pad if necessary
            submatrix = matrix[start_index:end_index]
            if submatrix.shape[0] < rows_per_submatrix and i != num_Banks - 1:
                pad_rows = rows_per_submatrix - submatrix.shape[0]
                submatrix = np.pad(submatrix, ((0, pad_rows), (0, 0)), mode='constant', constant_values=-1)
            submatrices.append(submatrix)
            start_index = end_index
        for i in range(num_Banks):
            pad_rows=num_rows-submatrices[i].shape[0]
            submatrices[i]=np.pad(submatrices[i], ((0, pad_rows), (0, 0)), mode='constant', constant_values=-1)
            
        return submatrices
