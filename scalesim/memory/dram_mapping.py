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

    def __call__(self, input):
        mappings={
            "Normal": self.Normal_Mapping,
            "Novel": self.novel_mapping

        }
        submatrices=mappings[self.type_of_Mapping](input)
        self.num_lines_per_bank=input.shape[0]//self.num_banks
        return submatrices
    
    """
    Define the mapping in this file and add the mapping to the call function. In the mappings dictionary.
    """

    def novel_mapping(self,matrix):
        num_banks=self.num_banks
        bank_acces={i:[] for i in range(num_banks)}
        
        partions_matrices=[[] for _ in range(num_banks)]
        unresolved=[]
        num_rows = matrix.shape[0]
        remainder=matrix.shape[0]%num_banks
        for i in range(0,len(matrix),num_banks):
            requests_in_cycle=matrix[i:num_banks+i]
            for j,data in enumerate(requests_in_cycle):
                for val in data:
                    in_Bank=0
                    for k in range(num_banks):
                        if val in bank_acces[k]:
                            in_Bank=1
                    if in_Bank==0:
                        bank_acces[j].append(val)
        if remainder!=0:
            requests_in_cycle=matrix[-remainder:]
            for j,data in enumerate(requests_in_cycle):
                for val in data:
                    in_Bank=0
                    for k in range(num_banks):
                        if val in bank_acces[k]:
                            in_Bank=1
                    if in_Bank==0:
                        bank_acces[j].append(val)

        for i in range(0,len(matrix),num_banks):
            sub_matrices=[[] for _ in range(num_banks)]
            requests_in_cycle=matrix[i:num_banks+i]
            for j,data in enumerate(requests_in_cycle):
                for val in data:
                    for k in range(num_banks):
                        if val in bank_acces[k]:
                            sub_matrices[k].append(val)
            if remainder!=0:
                requests_in_cycle=matrix[-remainder:]
                for j,data in enumerate(requests_in_cycle):
                    for val in data:
                        for k in range(num_banks):
                            if val in bank_acces[k]:
                                sub_matrices[k].append(val)
            for k in range(num_banks):
                if len(sub_matrices[k])==matrix.shape[1]:
                    partions_matrices[k].append(sub_matrices[k])
                elif len(sub_matrices[k])<matrix.shape[1]:
                    if len(sub_matrices[k])!=0:
                        sub_matrices[k]=sub_matrices[k]
                        remaining_values=matrix.shape[1]-len(sub_matrices[k])
                        for i in range(remaining_values):
                            sub_matrices[k].append(-1)
                        partions_matrices[k].append(sub_matrices[k])
                elif len(sub_matrices[k])>matrix.shape[1]:
                    remainder=len(sub_matrices[k])%matrix.shape[1]
                    for i in (0,len(sub_matrices[k]),matrix.shape[1]):
                        if i+matrix.shape[1]<len(sub_matrices[k]):
                            partions_matrices[k].append(sub_matrices[k][i:i+matrix.shape[1]])
                    if remainder!=0:
                        remaining=sub_matrices[k][-remainder:]
                        remaining_values=matrix.shape[1]-len(remaining)
                        for i in range(remaining_values):
                            remaining.append(-1)
                        partions_matrices[k].append(remaining)
        for i in range(num_banks):
            if(len(partions_matrices))<num_rows:
                pad_rows=num_rows-len(partions_matrices[i])
                values=matrix.shape[1]
                for rows in range(pad_rows):
                    partions_matrices[i].append([-1 for _ in range(values)])
            
        
        return partions_matrices

    def Normal_Mapping(self,matrix):
        # Get the number of rows in the matrix
        num_Banks=self.num_banks
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
            print(pad_rows)
            submatrices[i]=np.pad(submatrices[i], ((0, pad_rows), (0, 0)), mode='constant', constant_values=-1)
            
        return submatrices
