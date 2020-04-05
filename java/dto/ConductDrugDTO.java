package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("visit_conduct_drug")
public class ConductDrugDTO {
	@Primary
	@AutoInc
	@MysqlColName("id")
	public int conductDrugId;
	@MysqlColName("visit_conduct_id")
	public int conductId;
	public int iyakuhincode;
	public double amount;

	public static ConductDrugDTO copy(ConductDrugDTO src){
		ConductDrugDTO dst = new ConductDrugDTO();
		dst.conductDrugId = src.conductDrugId;
		dst.conductId = src.conductId;
		dst.iyakuhincode = src.iyakuhincode;
		dst.amount = src.amount;
		return dst;
	}
	
	@Override
	public String toString(){
		return "ConductDrugDTO[" +
			"conductDrugId=" + conductDrugId + ", " +
			"conductId=" + conductId + ", " +
			"iyakuhincode=" + iyakuhincode + ", " +
			"amount=" + amount + 
		"]";
	}
}