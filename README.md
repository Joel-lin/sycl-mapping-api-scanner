# sycl-mapping-api-scanner
A utility to help analyze CUDA-SYCL migration projects and provide a summary report regarding the current support status of SYCL mapping/migration APIs tracked by Intel SYCLomatic open source project. The database of CUDA migration APIs is stored under https://github.com/oneapi-src/SYCLomatic/tree/SYCLomatic/docs/dev_guide/api-mapping-status

# How to run 
>
> python sycl-mapping-APIs-scanner.py

Brief:
  This utility mainly scans the preset filetypes(.cu, .cuh, .c, .h, .cpp, .hpp, .py and etc..) to find unsupported APIs listed by SYCLomatic project. Reference link(2023-10-12):https://oneapi-src.github.io/SYCLomatic/dev_guide/api-mapping-status.html

  Please specify the folder path using the -p parameter.

  -p <projectfolderpath>     specify the CUDA migration projects folder path.
  --printcsv                 print report(experimental)

Example usages:

    1. sycl_mapping_APIs_scanner -p <cudaproject_folderpath>

    2. sycl_mapping_APIs_scanner --printcsv <examplereport.csv>
