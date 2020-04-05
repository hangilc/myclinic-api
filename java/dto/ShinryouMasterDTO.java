package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("shinryoukoui_master_arch")
public class ShinryouMasterDTO {
	@Primary
	public int shinryoucode;
	@Primary
	@TypeHint({"date"})
	public String validFrom;
	public String name;
	@TypeHint({"floatFormatStorage"})
	public int tensuu;
	public char tensuuShikibetsu;
	public String shuukeisaki;
	public String houkatsukensa;
	public char oushinkubun; // not used (2018-10-31)
	@MysqlColName("kensagroup")
	public String kensaGroup;
	@TypeHint({"date", "nullable"})
	public String validUpto;

	@Override
	public String toString(){
		return "ShinryouMasterDTO[" +
			"shinryoucode=" + shinryoucode + "," +
			"validFrom=" + validFrom + "," +
			"name=" + name + "," +
			"tensuu=" + tensuu + "," +
			"tensuuShikibetsu=" + tensuuShikibetsu + "," +
			"shuukeisaki=" + shuukeisaki + "," +
			"houkatsukensa=" + houkatsukensa + "," +
			"oushinkubun=" + oushinkubun + "," +
			"kensaGroup=" + kensaGroup + "," +
			"validUpto=" + validUpto +
		"]";
	}
}