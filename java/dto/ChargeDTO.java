package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("visit_charge")
public class ChargeDTO {
	@Primary
	public int visitId;
	public int charge;

	public static ChargeDTO create(int visitId, int charge){
		ChargeDTO dst = new ChargeDTO();
		dst.visitId = visitId;
		dst.charge = charge;
		return dst;
	}

	public static ChargeDTO copy(ChargeDTO src){
		ChargeDTO dst = new ChargeDTO();
		dst.visitId = src.visitId;
		dst.charge = src.charge;
		return dst;
	}

	@Override
	public String toString() {
		return "ChargeDTO{" +
				"visitId=" + visitId +
				", charge=" + charge +
				'}';
	}
}