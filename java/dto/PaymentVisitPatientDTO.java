package dev.myclinic.dto;

/**
 * Created by hangil on 2017/05/20.
 */
public class PaymentVisitPatientDTO {
    public PaymentDTO payment;
    public VisitDTO visit;
    public PatientDTO patient;

    @Override
    public String toString() {
        return "PaymentVisitPatientDTO{" +
                "payment=" + payment +
                ", visit=" + visit +
                ", patient=" + patient +
                '}';
    }
}
