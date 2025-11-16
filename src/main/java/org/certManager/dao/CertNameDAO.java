package org.certManager.dao;


import java.util.List;
import java.util.Optional;

import org.certManager.model.CertName;

public interface CertNameDAO {
    
    CertName createCertName(CertName certName);// Create new Certificate Name
    Optional<CertName> getCertNameById(int id); // Get Certificate Name by ID
    Optional<CertName> getCertNameByName(String name); // Get Certificate Name by Name
    List<CertName> getAllCertNames(); // Get all Certificate Names
    void updateCertName(CertName certName); // Update Certificate Name
    
    void deleteCertName(int id); // Delete Certificate Name by ID

}