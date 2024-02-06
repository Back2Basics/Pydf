# pydf_demo.py

# copyright (c) 2024 Ray Lutz



import sys

sys.path.append('..')

from Pydf.md_demo import md_code_seg # pr, 


def main():

    md_report = "# Python Daffodil (Pydf) Demo\n\n"
    
    md_report += """ Python Daffodil (Pydf) is a simple and flexible dataframe package for use with Python.
This page will demonstrate the functionality of Daffodil by showing actual code and results of 
running that code. Daffodil is a good match for many common algorithms in data pipelines and other conversion use cases.
    
For more information about Daffodil, see [https://github.com/raylutz/Pydf/blob/main/README.md]()

This page is the result of using simple "notebook" functionality (md_demo.py)
which will create a markdown "notebook" report by printing a code block and then run and capture the result. The report can
be viewed directly or converted to HTML for use on a static website.

"""

    md_report += md_code_seg('Create a new empty table')
    from Pydf.Pydf import Pydf
    
    my_pydf = Pydf()
    
    md_report += f"The empty my_pydf:\n{my_pydf}\n"
    md_report += f"{bool(my_pydf)=}\n"
    
    # note here that testing my_pydf produces "False" if there is nothing in the array,
    # even though the instance itself exists.
    
    md_report += md_code_seg('Append some rows to the pydf object') + "\n" 
    # here we append dictionaries to the pydf array.
    # The column header is determined from the first dictionary added if it
    # is not otherwise initialized.
    
    my_pydf.append({'A': 1,  'B': 2, 'C': 3})  
    my_pydf.append({'A': 5,  'C': 7, 'B': 6})  
    my_pydf.append({'C': 10, 'A': 8, 'B': 9})
    
    md_report += f"The appended my_pydf:\n{my_pydf}\n"
    # notice that when each row is appended, the columns are respected,
    # even if the data is provided in a different order.

    md_report += md_code_seg('Read and write individual cells by row,col indices') + "\n" 
    # replace value at row 2, col 1 (i.e. 9) with value from row 1, col 0 (i.e. 5)
    # multiplied by the value in cell [2,2] (i.e. 10) resulting in 50 at [2,1].
    # Note that row and column indices start at 0, and are in row, col order (not x,y).
    
    my_pydf[2,1] = my_pydf[1,0] * my_pydf[2,2]

    md_report += f"The modified my_pydf:\n{my_pydf}\n"

    md_report += md_code_seg('Read columns and rows') + "\n" 

    # when accessing a column or row using indices will return a list.
    # Columns can be indexed by number or by column name, which must be a str.
    
    col_2 = my_pydf[:,2]
    row_1 = my_pydf[1]
    col_B = my_pydf[:,'B']

    md_report += f"- {col_2=}\n- {row_1=}\n- {col_B=}\n"    

    md_report += md_code_seg('Read rows and columns using methods') + "\n" 
    # when using methods to access: columns are returned as lists, 
    # and rows are returned as dicts.
    
    col_2 = my_pydf.icol(2)
    row_1 = my_pydf.irow(1)
    col_B = my_pydf.col('B')

    md_report += f"- {col_2=}\n- {row_1=}\n- {col_B=}\n"
    
    md_report += md_code_seg('Insert a new column "Category" on left, and make it the keyfield') + "\n" 
    """ Rows in a Pydf instance can be indexed using an existing column, by specifying that column as the keyfield.
        This will create the keydict kd which creates the index from each value. It must have unique hashable values. 
        The keyfield can be set at the same time the column is added.
        The key dictionary kd is maintained during all pydf manipulations.
        A pydf generated by selecting some rows from the source pydf will maintain the same keyfield, and .keys()
        method will return the subset of keys that exist in that pydf.
    """

    # Add a column on the left (icol=0) and set it as the keyfield.

    my_pydf.insert_icol(icol=0, 
            col_la=['house', 'car', 'boat'], 
            colname='Category', 
            keyfield='Category')

    md_report += f"my_pydf:\n{my_pydf}\n"
    

    md_report += md_code_seg('Select a record by the key:') + "\n"
    """ Selecting one record by the key will return a dictionary.
    """

    da = my_pydf.select_record_da('car')

    md_report += f"Result:\n\n- {da=}\n"
    

    md_report += md_code_seg('Append more records from a lod') + "\n"
    """ When records are appended from a lod (list of dict), they are appended as rows,
    the columns are respected, and the kd is updated. Using a pydf
    instance is about 1/3 the size of an equivalent lod because the dictionary
    keys are not repeated for each row in the array.
    """

    lod = [{'Category': 'mall',  'A': 11,  'B': 12, 'C': 13},
           {'Category': 'van',   'A': 14,  'B': 15, 'C': 16},
           {'A': 17,  'C': 19, 'Category': 'condo', 'B': 18},
          ]

    my_pydf.append(lod)  
    
    md_report += f"The appended my_pydf:\n{my_pydf}\n"

    md_report += md_code_seg('Update records') + "\n"
    """ updating records mutates the existing pydf instance, and works
        like a database table. The keyvalue in the designated keyfield
        determines which record is updated. This uses the append()
        method because appending respects the keyfield, if it is defined.
    """
    
    lod = [{'Category': 'car',  'A': 25,  'B': 26, 'C': 27},
           {'Category': 'house', 'A': 31,  'B': 32, 'C': 33},
          ]

    my_pydf.append(lod)  
    
    md_report += f"The updated my_pydf:\n{my_pydf}\n"

    md_report += md_code_seg('Add a column "is_vehicle"') + "\n" 
    my_pydf.insert_col(colname='is_vehicle', col_la=[0,1,1,0,1,0], icol=1)

    md_report += f"The updated my_pydf:\n{my_pydf}\n"
    
    md_report += md_code_seg('pydf bool') + "\n" 
    """ For pydf, bool() simply determines if the pydf exists and is not empty.
        This functionality makes it easy to use `if pydf:` to test if the
        pydf is not None and is not empty. This does not evaluate the __content__
        of the array, only whether contents exists in the array. Thus,
        an array with 0, False, or '' still is regarded as having contents.
        In contrast, Pandas raises an error if you try: ```bool(df)```.
        Normally, a lol structure that has an internal empty list is True,
        i.e. `bool([[]])` will evaluate as true while `bool(Pydf(lol=[[]]))` is False. 
    """
    md_report += f"- {bool(my_pydf)=}\n"
    md_report += f"- {bool(Pydf(lol=[]))=}\n"
    md_report += f"- {bool(Pydf(lol=[[]]))=}\n"
    md_report += f"- {bool(Pydf(lol=[[0]]))=}\n"
    md_report += f"- {bool(Pydf(lol=[['']]))=}\n"
    md_report += f"- {bool(Pydf(lol=[[False]]))=}\n\n"
    
    md_report += md_code_seg('pydf attributes') + "\n" 
    md_report += f"- {len(my_pydf)=}\n"
    md_report += f"- {my_pydf.len()=}\n"
    md_report += f"- {my_pydf.shape()=}\n"
    md_report += f"- {my_pydf.columns()=}\n"
    md_report += f"- {my_pydf.keys()=}\n"
    
    md_report += md_code_seg('get_existing_keys') + "\n"
    """ check a list of keys to see if they are defined in the pydf instance 
    """
    existing_keys_ls = my_pydf.get_existing_keys(['house', 'boat', 'RV'])
    md_report += f"- {existing_keys_ls=}\n"
    
    md_report += md_code_seg('select_records_pydf') + "\n"
    """ select multiple records using a list of keys and create a new pydf instance. 
        Also orders the records according to the list provided.
    """
    wheels_pydf = my_pydf.select_records_pydf(['van', 'car'])
    md_report += f"wheels_pydf:\n{wheels_pydf}\n"

    md_report += md_code_seg('select_by_dict') + "\n"
    """ select_by_dict offers a way to select for all exact matches to dict,
        or if inverse is set, the set that does not match.
    """
    vehicles_pydf  = my_pydf.select_by_dict({'is_vehicle':1})
    buildings_pydf = my_pydf.select_by_dict({'is_vehicle':0})
    # or
    buildings_pydf = my_pydf.select_by_dict({'is_vehicle':1}, inverse=True)

    md_report += f"vehicles_pydf:\n{vehicles_pydf}\nbuildings_pydf:\n{buildings_pydf}\n"

    md_report += md_code_seg("use `select_where` to select rows where column 'C' is over 20") + "\n" 
    high_c_pydf = my_pydf.select_where(lambda row: bool(row['C'] > 20))

    md_report += f"high_c_pydf:\n{high_c_pydf}\n"

    md_report += md_code_seg("convert to pandas DataFrame") + "\n" 
    my_df = my_pydf.to_pandas_df()

    md_report += f"\nConverted DataFrame:\n```\n{my_df}\n```\n"

    md_report += md_code_seg("Add index column 'idx' to the dataframe at the left, starting at 0.") + "\n" 
    my_pydf.insert_idx_col(colname='idx') #, icol=0, startat=0)

    md_report += f"\nModified pydf:\n{my_pydf}\n\n"

    # md_report += md.md_code_seg("convert from pandas DataFrame") + "\n" 
    # recovered_pydf = Pydf.from_pandas_df(my_df, keyfield='Category')

    # md_report += f"\nConvert Back:\n```{recovered_pydf}```\n"

    md_code_seg()    # end marker
    #===================================

    print(md_report)

    with open('..\docs\pydf_demo.md', 'w') as file:
        file.write(md_report)


if __name__ == '__main__':
    main()    