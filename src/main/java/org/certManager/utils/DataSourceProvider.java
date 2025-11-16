package org.certManager.utils;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

import javax.sql.DataSource;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class DataSourceProvider {

    private static HikariDataSource dataSource;

    private DataSourceProvider() { }

    public static synchronized DataSource getDataSource() {
        if (dataSource == null) {
            Properties props = new Properties();
            try (InputStream is = DataSourceProvider.class.getClassLoader().getResourceAsStream("db.properties")) {
                if (is == null) {
                    throw new RuntimeException("db.properties not found on classpath");
                }
                props.load(is);
            } catch (IOException e) {
                throw new RuntimeException("Error loading db.properties", e);
            }

            HikariConfig config = new HikariConfig();
            config.setJdbcUrl(props.getProperty("jdbcUrl"));
            config.setUsername(props.getProperty("username"));
            config.setPassword(props.getProperty("password"));

            String maxPool = props.getProperty("maximumPoolSize");
            if (maxPool != null) config.setMaximumPoolSize(Integer.parseInt(maxPool));
            String minIdle = props.getProperty("minimumIdle");
            if (minIdle != null) config.setMinimumIdle(Integer.parseInt(minIdle));
            String connTimeout = props.getProperty("connectionTimeout");
            if (connTimeout != null) config.setConnectionTimeout(Long.parseLong(connTimeout));
            String idleTimeout = props.getProperty("idleTimeout");
            if (idleTimeout != null) config.setIdleTimeout(Long.parseLong(idleTimeout));
            String maxLifetime = props.getProperty("maxLifetime");
            if (maxLifetime != null) config.setMaxLifetime(Long.parseLong(maxLifetime));

            dataSource = new HikariDataSource(config);
        }
        return dataSource;
    }

    public static synchronized void close() {
        if (dataSource != null) {
            dataSource.close();
            dataSource = null;
        }
    }
}
