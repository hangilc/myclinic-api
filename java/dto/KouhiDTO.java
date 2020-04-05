package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("kouhi")
public class KouhiDTO {
	@Primary
	@AutoInc
	public int kouhiId;
	public int patientId;
	public int futansha;
	public int jukyuusha;
	@TypeHint({"date"})
	public String validFrom;
	@TypeHint({"date", "nullable"})
	public String validUpto;

	public KouhiDTO copy(){
		KouhiDTO dst = new KouhiDTO();
		dst.kouhiId = kouhiId;
		dst.patientId = patientId;
		dst.futansha = futansha;
		dst.jukyuusha = jukyuusha;
		dst.validFrom = validFrom;
		dst.validUpto = validUpto;
		return dst;
	}

	public void assign(KouhiDTO src){
		kouhiId = src.kouhiId;
		patientId = src.patientId;
		futansha = src.futansha;
		jukyuusha = src.jukyuusha;
		validFrom = src.validFrom;
		validUpto = src.validUpto;
	}

	@Override
	public String toString(){
		return "KouhiDTO[" + 
			"kouhiId=" + kouhiId + "," + 
			"patientId=" + patientId + "," + 
			"futansha=" + futansha + "," + 
			"jukyuusha=" + jukyuusha + "," + 
			"validFrom=" + validFrom + "," + 
			"validUpto=" + validUpto + 
		"]";
	}
}