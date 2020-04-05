package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("visit_conduct")
public class ConductDTO {
	@Primary @AutoInc
	@MysqlColName("id")
	public int conductId;
	public int visitId;
	public int kind;

	public static ConductDTO copy(ConductDTO src){
		ConductDTO dst = new ConductDTO();
		dst.conductId = src.conductId;
		dst.visitId = src.visitId;
		dst.kind = src.kind;
		return dst;
	}

	@Override
	public String toString(){
		return "ConductDTO[" +
		"conductId=" + conductId + "," +
		"visitId=" + visitId + "," +
		"kind=" + kind + //"," +
		"]";
	}
}