package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("visit_gazou_label")
public class GazouLabelDTO {
	@Primary
	@MysqlColName("visit_conduct_id")
	public int conductId;
	public String label;

	public static GazouLabelDTO copy(GazouLabelDTO src){
		GazouLabelDTO dst = new GazouLabelDTO();
		dst.conductId = src.conductId;
		dst.label = src.label;
		return dst;
	}

	@Override
	public String toString(){
		return "GazouLabelDTO[" +
			"conductId=" + conductId + "," +
			"label=" + label +
		"]";
	}
}