# simple-CDCL
Simple implementation of CDCL by Python
## 0. 环境配置与启动
### 0.1 环境配置

Python >= 3.5
### 0.2 How to run
```
python solver.py
```
Modify the file_path in solver.py to run the code by the specified .cnf input file
## 1.目录结构
```
│  .gitignore  // Git ignore file
│  LICENSE     // copyright license
│  models.py   // implementation of Literal, Clause, Cnf, Node, Trail
│  parse.py    // implementation of cnf file parser
│  README.md   // readme file
│  solver.py   // implementation of SAT solver used CDCL
│  test.py     // test code for backtrace
│  test1.py    // test code for bcp
│  utils.py    // common function used as util
│  
├─raw      // base input file path
│      
└─result   // base result file path

```