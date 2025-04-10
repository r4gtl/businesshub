import net.sf.jasperreports.engine.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Map;

public class ReportGenerator {
    public static void main(String[] args) {
        System.setProperty("net.sf.jasperreports.extension.registry.factory.fonts",
                "net.sf.jasperreports.engine.fonts.SimpleFontExtensionsRegistryFactory");
        System.setProperty("net.sf.jasperreports.extension.simple.font.families.dejavusans",
                "/opt/jasperreports/fonts/fonts.xml");
        String[] fonts = java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment().getAvailableFontFamilyNames();
        System.out.println("Font disponibili:");
        for (String font : fonts) {
            System.out.println(font);
        }

        try {
            if (args.length < 6) {
                System.err.println(
                        "Usage: java ReportGenerator <template_path> <output_path> <db_url> <db_user> <db_password> [param1=value1 param2=value2 ...]");
                System.exit(1);
            }

            String templatePath = args[0];
            String outputPath = args[1];
            String dbUrl = args[2];
            String dbUser = args[3];
            String dbPassword = args[4];

            // Debugging info
            System.out.println("Template path: " + templatePath);
            System.out.println("Output path: " + outputPath);
            System.out.println("Database URL: " + dbUrl);

            // Create parameters map
            Map<String, Object> parameters = new HashMap<>();
            for (int i = 5; i < args.length; i++) {
                String[] param = args[i].split("=", 2);
                if (param.length == 2) {
                    // Convert PK parameter to Integer
                    if (param[0].equals("PK")) {
                        try {
                            long pkValue = Long.parseLong(param[1]);
                            parameters.put(param[0], pkValue);
                            System.out.println("Parameter: " + param[0] + " = " + pkValue + " (Long)");
                        } catch (NumberFormatException e) {
                            System.err.println("Error: PK parameter must be a number");
                            System.exit(1);
                        }
                    } else {
                        parameters.put(param[0], param[1]);
                        System.out.println("Parameter: " + param[0] + " = " + param[1]);
                    }
                }
            }

            // Explicitly load the JDBC driver
            Class.forName("org.postgresql.Driver");
            System.out.println("PostgreSQL JDBC driver loaded.");

            // Connect to the database
            System.out.println("Connecting to database: " + dbUrl);
            Connection connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
            System.out.println("Database connection established.");

            // Test query più dettagliata
            System.out.println("Executing test query...");
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt
                    .executeQuery("SELECT id, numero_interno, plafond FROM documenti_dichiarazioneintento WHERE id = "
                            + parameters.get("PK"));
            if (rs.next()) {
                System.out.println("Record found: ID=" + rs.getLong("id") +
                        ", numero_interno=" + rs.getInt("numero_interno") +
                        ", plafond=" + rs.getBigDecimal("plafond"));
            } else {
                System.out.println("No records found with PK=" + parameters.get("PK"));
            }
            rs.close();
            stmt.close();

            // Compile and generate the report with database connection
            System.out.println("Filling report with parameters: " + parameters);
            JasperPrint jasperPrint = JasperFillManager.fillReport(templatePath, parameters, connection);

            System.out.println("Report compiled successfully.");

            System.out.println("Number of pages in report: " + jasperPrint.getPages().size());
            if (jasperPrint.getPages().size() > 0) {
                System.out.println("Page height: " + jasperPrint.getPageHeight());
                System.out.println("Page width: " + jasperPrint.getPageWidth());
            }

            JasperExportManager.exportReportToPdfFile(jasperPrint, outputPath);
            System.out.println("Report generated successfully: " + outputPath);

            // Close the database connection
            connection.close();
            System.exit(0);
        } catch (Exception e) {
            System.err.println("Error generating report: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}