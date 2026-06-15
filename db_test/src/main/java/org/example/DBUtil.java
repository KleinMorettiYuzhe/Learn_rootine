package org.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBUtil {
    private static final String URL = "jdbc:mysql://localhost:3306/test?useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true&characterEncoding=utf8";
    private static final String USER = "root";
    private static final String PASSWORD = "123456";
    private static Connection conn = null;

    public static Connection getConn() {
        try {
            // 强制加载驱动（Tomcat里有时候Class.forName不生效）
            Class.forName("com.mysql.cj.jdbc.Driver");
            System.out.println("驱动加载成功");
            conn = DriverManager.getConnection(URL, USER, PASSWORD);
            System.out.println("连接成功");
        } catch (ClassNotFoundException e) {
            System.err.println("❌ 驱动类找不到：" + e.getMessage());
            e.printStackTrace();
        } catch (SQLException e) {
            System.err.println("❌ SQL异常：错误码=" + e.getErrorCode() + ", 信息=" + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("❌ 未知异常：" + e.getMessage());
            e.printStackTrace();
        }
        return conn;
    }

    public static void closeConn(Connection conn) {
        if (conn != null) {
            try {
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        Connection conn = DBUtil.getConn();
        if (conn != null) {
            System.out.println("本地main方法测试连接成功！");
            DBUtil.closeConn(conn);
        } else {
            System.out.println("本地main方法测试连接失败！");
        }
    }
}