package dev.myclinic.dto;

public class TextVisitPatientDTO {
    public TextDTO text;
    public VisitDTO visit;
    public PatientDTO patient;

    @Override
    public String toString() {
        return "TextVisitPatientDTO{" +
                "text=" + text +
                ", visit=" + visit +
                ", patient=" + patient +
                '}';
    }
}
