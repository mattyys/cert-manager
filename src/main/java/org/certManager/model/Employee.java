package org.certManager.model;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Employee {
    
    private String employeeName;
    private String employeeId;
    private String employeeSurname;
    private String phoneNumber;
    private boolean isIncludedInMdp;
    private Company company;
    private IsActiveEmployee isActiveEmployee;
    private List<CertExpiration> certExpirations;
    private Position position;
    

}
