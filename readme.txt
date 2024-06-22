使用须知：
①程序分为reversetcpclient.py与reversetcpserver.py共两个文件，一定要先开启服务器程序才能使用客户端程序。
②程序编写时使用python版本为3.11。
③服务器程序直接运行即可，客户端程序则需要在命令行输入5个参数：服务器IP、服务器端口号、文件路径、消息最小字节数、消息最大字节数。
④服务器IP为开启服务器程序的主机的IP（如就在本机实验，localhost也行）；端口号为10101；文件内容必须是acsii能够显示的字符集（如纯英文）；消息最大或最小字节数是指在客户端传递消息时，数据内容里包含的字节长度范围，为左闭右闭区间。

程序介绍：
①本程序使用TCP的方法传递数据。客户端以随机长度的方式（模拟不定长）读取文件里的数据并打包传递，服务器将客户端传来的字符数据全部逆序后发回，最后客户端将其显示并另存为一个文件。
②交互过程共有4种报文：intialization、agree、reverseRequest、reverseAnswer。
③intialization：type（2字节）+N（4字节）。type为1指定该报文类型，N是客户端接下来一共要请求的reverseRequest的次数。
④agree：type（2字节）。type为2指定该报文类型，表示同意连接并进行处理。
⑤reverseRequest：type（2字节）+Length（4字节）+Data（不定长）。type为3指定该报文类型，Length表示Data的长度，以1字节为单位，Data便是客户端传递的字符数据。
⑥reverseAnswer：type（2字节）+Length（4字节）+reverseData（不定长）。type为4指定该报文类型，Length表示reverseData的长度，以1字节为单位，reverseData便是逆序过后的字符数据。
