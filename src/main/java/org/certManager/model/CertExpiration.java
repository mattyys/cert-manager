package org.certManager.model;

import java.time.LocalDate;

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
public class CertExpiration {
    
	
    private CertName certName;
    private LocalDate expirationDate;
    private LocalDate dateMade;
    

}
