package org.certManager.dao;

import java.util.List;
import java.util.Optional;

import org.certManager.model.Employee;

public interface EmployeeDAO {
    
    Employee createEmployee(Employee employee);
    Optional<Employee> getEMployeeById(int employeeId);
    Optional<Employee> getEmployeeByName(String employeeName);
    List<Employee> getAllEmployees();
    List<Employee> getEmployeesByCertExpirationDate();// Get employees with certificates nearing expiration 30 days
    void updateEmployee(Employee employee);
    

}
