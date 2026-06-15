<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>DB Test 首页</title>
</head>
<body>
<h1>数据库连接测试Demo</h1>
<p>点击下方链接测试MySQL连接：</p>
<a href="${pageContext.request.contextPath}/dbTest">👉 测试数据库连接</a>
<p>当前项目路径：${pageContext.request.contextPath}</p>
</body>
</html>