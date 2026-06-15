package org.example;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;

/**
 * 数据库测试Servlet
 * 包名：org.example
 * 访问路径：/dbTest
 */
@WebServlet("/dbTest") // 核心：注解路径正确
public class DBTestServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // 解决中文乱码
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();

        out.write("<html>");
        out.write("<head><title>数据库连接测试</title></head>");
        out.write("<body>");
        out.write("<h1>MySQL连接测试</h1>");

        // 测试连接
        Connection conn = DBUtil.getConn();
        if (conn != null) {
            out.write("<h2 style='color:green;'>✅ 连接成功！</h2>");
            DBUtil.closeConn(conn);
        } else {
            out.write("<h2 style='color:red;'>❌ 连接失败！</h2>");
            out.write("<p>排查方向：</p>");
            out.write("<ul>");
            out.write("<li>1. MySQL服务是否启动（cmd执行：net start mysql80）</li>");
            out.write("<li>2. test数据库是否创建（MySQL执行：CREATE DATABASE test;）</li>");
            out.write("<li>3. 密码是否为123456，或执行SQL：ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';</li>");
            out.write("</ul>");
        }

        out.write("</body>");
        out.write("</html>");
        out.close();
    }
}