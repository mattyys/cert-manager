package org.certManager.dao;

import java.util.List;
import java.util.Optional;

import org.certManager.model.Company;

public interface CompanyDAO {
    
    Company createCompany(String name);
    Optional<Company> getCompanyById(int id);
    Optional<Company> getCompanyByName(String name);
    List<Company> getAllCompanies();
    void updateCompany(Company company);
    
    void deleteCompany(int id);

}
