package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("visit_conduct_shinryou")
public class ConductShinryouDTO {
	@Primary
	@AutoInc
	@MysqlColName("id")
	public int conductShinryouId;
	@MysqlColName("visit_conduct_id")
	public int conductId;
	public int shinryoucode;

	public static ConductShinryouDTO copy(ConductShinryouDTO src){
		ConductShinryouDTO dst = new ConductShinryouDTO();
		dst.conductShinryouId = src.conductShinryouId;
		dst.conductId = src.conductId;
		dst.shinryoucode = src.shinryoucode;
		return dst;
	}
	
	@Override
	public String toString(){
		return "ConductShinryouDTO[" +
			"conductShinryouId=" + conductShinryouId + ", " +
			"conductId=" + conductId + ", " +
			"shinryoucode=" + shinryoucode +
		"]";
	}
}
