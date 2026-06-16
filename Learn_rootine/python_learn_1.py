# # 一些快捷键
# # ctrl + /  # 注释
# # ctrl + alt + l  # 整理代码
# # ctrl + alt + n  # 运行当前文件
# # ctrl + alt + t  # 运行当前行
# # ctrl + alt + m  # 运行当前方法
# # ctrl + d        # 复制当前行



# # 1.
# # 字面量（即定值，如常数和字符串）
# print(100)  # 整数
# print(3.14)  # 浮点数
# print(True)  # 布尔值(首字母大写)
# # 布尔类型本质为int型，True的值为1，False的值为0
# print(False)  # 布尔值
# print("hello world")  # 字符串 (单引号或双引号等效,三引号可以跨越多行字符串
    # respect = """尊敬的朋友，
    # 你好！
    # """(三引号的案例)
# )
# print(None)  # 空值

# # python中对大小写严格要求，一旦写错会抛出异常




# # 2.
# # 变量（视作容器，将可变的数据存储在容器中，变量名必须以字母开头，可包含数字，下划线）
# # Python是动态类型语言，变量不需要声明类型，直接赋值即可使用，可以存储不同类型的数据(实际开发中推荐只使用一种类型的数据，避免类型冲突)

# num = 1314  # 将整数1314赋值给变量num
# print(num)  # 输出变量num的值

# num = num + 1  # 将变量num的值加1，并将结果重新赋值给num
# print(num)  # 输出变量num的值，此时为1315

# num = "在一起"  # 将字符串"在一起"赋值给变量num，覆盖之前的整数值
# print(num)  # 输出变量num的值，此时为字符串"在一起"

# # python中输出多项内容时，可以使用逗号分隔，输出时会自动添加空格

# print("我","喜欢","你")
# a = 10
# b = 20
# print("a =", a, "b =", b)  # 输出变量a和b的值






# 3.
# 数据类型
# type() 函数：可以查看变量的类型
print(type(100))  # <class 'int'>
print(type(3.14))  # <class 'float'>
print(type(True))  # <class 'bool'>
print(type("hello world"))  # <class 'str'>
print(type(None))  # <class 'NoneType'>
num = "在一起"
print(type(num))   #变量本身没有类型，但它的值有类型，此时num的值为字符串"在一起"，所以输出<class 'str'>

# isinstance函数：isinstance(数据, 类型)  # 判断数据是否为某种类型，返回布尔值
print(isinstance(100, int))  # True

# 转义字符： \'(避免单引号在英文缩写it's被解释为字符串结束符)  \"  \n(换行)  \t(制表符) \\(反斜杠本身)