package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("tokuteikizai_master_arch")
public class KizaiMasterDTO {
	@Primary
	public int kizaicode;
	@Primary
	@TypeHint({"date"})
	public String validFrom;
	public String name;
	public String yomi;
	public String unit;
	public double kingaku;
	@TypeHint({"date", "nullable"})
	public String validUpto;

	@Override
	public String toString() {
		return "KizaiMasterDTO{" +
				"kizaicode=" + kizaicode +
				", validFrom='" + validFrom + '\'' +
				", name='" + name + '\'' +
				", yomi='" + yomi + '\'' +
				", unit='" + unit + '\'' +
				", kingaku=" + kingaku +
				", validUpto='" + validUpto + '\'' +
				'}';
	}
}