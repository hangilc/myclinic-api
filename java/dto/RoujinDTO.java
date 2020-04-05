package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("hoken_roujin")
public class RoujinDTO {
	@Primary
	@AutoInc
	public int roujinId;
	public int patientId;
	public int shichouson;
	public int jukyuusha;
	public int futanWari;
	@TypeHint({"date"})
	public String validFrom;
	@TypeHint({"date", "nullable"})
	public String validUpto;

	public RoujinDTO copy(){
		RoujinDTO dst = new RoujinDTO();
		dst.roujinId = roujinId;
		dst.patientId = patientId;
		dst.shichouson = shichouson;
		dst.jukyuusha = jukyuusha;
		dst.futanWari = futanWari;
		dst.validFrom = validFrom;
		dst.validUpto = validUpto;
		return dst;
	}

	public void assign(RoujinDTO src){
		roujinId = src.roujinId;
		patientId = src.patientId;
		shichouson = src.shichouson;
		jukyuusha = src.jukyuusha;
		futanWari = src.futanWari;
		validFrom = src.validFrom;
		validUpto = src.validUpto;
	}

	@Override
	public String toString(){
		return "RoujinDTO[" +
			"roujinId=" + roujinId + "," +
			"patientId=" + patientId + "," +
			"shichouson=" + shichouson + "," +
			"jukyuusha=" + jukyuusha + "," +
			"futanWari=" + futanWari + "," +
			"validFrom=" + validFrom + "," +
			"validUpto=" + validUpto +
		"]";
	}
}