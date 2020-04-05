package dev.myclinic.dto;

public class VisitPatientDTO {
	public VisitDTO visit;
	public PatientDTO patient;

	@Override
	public String toString() {
		return "VisitPatientDTO{" +
				"visit=" + visit +
				", patient=" + patient +
				'}';
	}

	public static VisitPatientDTO create(VisitDTO visit, PatientDTO patient){
		VisitPatientDTO result = new VisitPatientDTO();
		result.visit = visit;
		result.patient = patient;
		return result;
	}
}