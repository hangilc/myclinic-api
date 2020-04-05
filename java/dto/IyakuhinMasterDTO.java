package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("iyakuhin_master_arch")
public class IyakuhinMasterDTO {
	@Primary
	public int iyakuhincode;
	@Primary
	@TypeHint({"date"})
	public String validFrom;
	public String name;
	public String yomi;
	public String unit;
	public double yakka;
	public char madoku;
	public char kouhatsu;
	public char zaikei;
	@TypeHint({"date", "nullable"})
	public String validUpto;

	@Override
	public String toString(){
		return "IyakuhinMasterDTO[" + 
			"iyakuhincode=" + iyakuhincode + "," +
			"validFrom=" + validFrom + "," +
			"name=" + name + "," +
			"yomi=" + yomi + "," +
			"unit=" + unit + "," +
			"yakka=" + yakka + "," +
			"madoku=" + madoku + "," +
			"kouhatsu=" + kouhatsu + "," +
			"zaikei=" + zaikei + "," +
			"validUpto=" + validUpto +
		"]";
	}
}