package dev.myclinic.dto;

public class VisitFull2PatientDTO {

    public VisitFull2DTO visitFull;
    public PatientDTO patient;

    @Override
    public String toString() {
        return "VisitFull2PatientDTO{" +
                "visitFull=" + visitFull +
                ", patient=" + patient +
                '}';
    }
}
