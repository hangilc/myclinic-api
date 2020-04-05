package dev.myclinic.dto;

public class DrugFullDTO {
	public DrugDTO drug;
	public IyakuhinMasterDTO master;

	public static DrugFullDTO copy(DrugFullDTO src){
		DrugFullDTO dst = new DrugFullDTO();
		dst.drug = src.drug;
		dst.master = src.master;
		return dst;
	}

	public static DrugFullDTO create(DrugDTO drug, IyakuhinMasterDTO master){
		DrugFullDTO result = new DrugFullDTO();
		result.drug = drug;
		result.master = master;
		return result;
	}

	@Override
	public String toString() {
		return "DrugFullDTO{" +
				"drug=" + drug +
				", master=" + master +
				'}';
	}
}