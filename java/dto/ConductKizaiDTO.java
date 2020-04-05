package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("visit_conduct_kizai")
public class ConductKizaiDTO {
	@Primary @AutoInc
	@MysqlColName("id")
	public int conductKizaiId;
	@MysqlColName("visit_conduct_id")
	public int conductId;
	public int kizaicode;
	public double amount;

	public static ConductKizaiDTO copy(ConductKizaiDTO src){
		ConductKizaiDTO dst = new ConductKizaiDTO();
		dst.conductKizaiId = src.conductKizaiId;
		dst.conductId = src.conductId;
		dst.kizaicode = src.kizaicode;
		dst.amount = src.amount;
		return dst;
	}
	
	@Override
	public String toString(){
		return "ConductKizaiDTO[" +
			"conductKizaiId=" + conductKizaiId + ", " +
			"conductId=" + conductId + ", " +
			"kizaicode=" + kizaicode + ", " +
			"amount=" + amount + 
		"]";
	}
}