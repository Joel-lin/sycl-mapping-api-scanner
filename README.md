# sycl-mapping-api-scanner
A utility to help scan the sources of CUDA-SYCL migration projects and to provide a summary report listing unsupported APIs based on the support status of SYCL mapping/migration APIs tracked by Intel SYCLomatic open source project. The database of CUDA migration APIs is stored under https://github.com/oneapi-src/SYCLomatic/tree/SYCLomatic/docs/dev_guide/api-mapping-status

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

# example output

(base) root@root123:/home/root123# python sycl-mapping-APIs-scanner.py -p ./FBGEMM-main
root123_FBGEMM-main
report.csv should be generated.
folder name                                              root123_FBGEMM-main
occurence of total unsupported APIs                      43
-------------------------------------------------------------------------------
nvmlInit                                                 1
nvmlDeviceGetCount                                       1
nvmlDeviceGetHandleByIndex                               2
nvmlDeviceGetPciInfo                                     1
nvmlDeviceGetNvLinkState                                 1
nvmlDeviceGetNvLinkRemotePciInfo                         1
cudaDeviceGetByPCIBusId                                  1
cudaProfilerStart                                        5
cudaProfilerStop                                         5
__float2bfloat16_rn                                      3
asm                                                      16
asm volatile                                             6
-------------------------------------------------------------------------------
12 unique unsupported APIs(or ASMs) are likely being used in the project

--------------------------------------------------------------------------------------
You can use the following commands to find where are these unsupported APIs in codes lines numbers

    windows: findstr /S /N <APIs name> <projectfolderpath>\*.cu
    Linux: grep -rn <APIs name> <projectfolderpath>/*.cu

report_ASM.csv should be generated. use "--printcsv report_ASM.csv" to list unsupported PTXs if there is
(base) root@root123:/home/root123# dist/sycl-mapping-APIs-scanner-linux --printcsv report_ASM.csv
