# simple-CDCL

Simple implementation of CDCL by Python

## 0. 环境配置与启动

### 0.1 环境配置

Python >= 3.9

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

## 2.代码简介

实现了SAT问题的求解器，使用了完备性算法中的CDCL算法，大致分为布尔约束传播，冲突分析学习，回溯，决策四个部分

判断SAT的条件：当某组赋值下，CNF中所有子句取值都为真时，返回SAT和所有变量的赋值

判断UNSAT的条件：当决策层级为0时出现冲突，说明没有对任何变量决策的情况下就已冲突，返回UNSAT

### 2.1 布尔约束传播(BCP)

布尔约束传播(BCP)主要分为三步：

```
1.找到CNF中可能存在的单位子句
2.对CNF中每个子句进行BCP
3.重复上述过程直到CNF中不再有单位子句
```

BCP结束后如果有冲突，进入冲突分析学习(Conflict Analysis)，无冲突则进入决策(DECIDE)

### 2.2 冲突分析学习(Conflict Analysis)

冲突分析学习出现在某次BCP结束后发现冲突时，如果某个子句值为False（发现冲突），则进行UNSAT判断

若不满足UNSAT则开始冲突分析学习

概括地说，冲突分析实际是在含有冲突节点的蕴含图中寻找第一个唯一蕴含点，执行唯一蕴含冲突切割W=(A, B)，将切割后的A集合中有到B集合的边的顶点取并得到学习子句，将学习子句与原CNF取交进行学习。

实际上在代码中采用基于BFS的图遍历来查找第一个唯一蕴含点，思路如下：

```
1.根据冲突时的迹构建出G=(V,E)蕴含图，顶点集V包含所有被BCP的变量，边集E中的每条有向边(u,v)表示变量u是变量v被蕴含的原因
2.对这张蕴含图，从决策层最高的一个被决策的顶点出发进行BFS，BFS的每个层次中，若有某个层次存在一个顶点u，它相邻的上一层次的每个顶点都有边可达u，将First UIP记为顶点u，不断维护
3.BFS结束后最后的First UIP即为所求
```

然而以上思路遇到了两个问题：

```
1.变量较多的情况下，构建蕴含图需要相当大的空间开销
2.该思路仅仅利用了图的性质，而没有用到布尔式的特性，BFS也需要很大的时间开销
```

因此考虑从最终的冲突节点不断回溯，达到的第一个UIP即为First UIP，思路如下

```
1.记录产生冲突的子句下标，在该子句中寻找第一个属于当前决策层的变量u
2.在trail中找到该变量对应的节点，取出节点的reason对应的子句
3.将冲突子句和reason子句做并操作，得到一个新的冲突子句，该子句必定不含有u和¬u
4.重复1-3直至冲突子句中只剩下一个节点属于当前决策层的变量，此时得到的冲突子句即为学习子句
5.从冲突子句中取得第二大的决策层级作为回溯的目标层级，若都为同一层则回溯到0层
```

完成冲突分析学习后得到学习子句和目标回溯层，进入回溯(Backtrack)

### 2.3 回溯(Backtrack)

回溯部分的处理较为简单，主要分为两步：

```
1.根据唯一蕴含冲突切割得到的目标回溯层，删除大于该层的所有迹中节点
2.将当前决策层级设为目标回溯层次
```

回溯结束后回到BCP

### 2.4 决策(DECIDE)

决策阶段处理也较为简单，主要分为两步：

```
1.创建一个新的决策层（solver保存的决策层计数器+1）；
2.选择一个未被赋值的文字，将其文字或文字取非与CNF相交（表示该文字取真或假）
```
