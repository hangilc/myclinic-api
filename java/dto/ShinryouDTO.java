package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

import java.util.Objects;

@MysqlTable("visit_shinryou")
public class ShinryouDTO {
	@Primary
	@AutoInc
	public int shinryouId;
	public int visitId;
	public int shinryoucode;

	public static ShinryouDTO copy(ShinryouDTO src){
		ShinryouDTO dst = new ShinryouDTO();
		dst.shinryouId = src.shinryouId;
		dst.visitId = src.visitId;
		dst.shinryoucode = src.shinryoucode;
		return dst;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		ShinryouDTO that = (ShinryouDTO) o;
		return shinryouId == that.shinryouId &&
				visitId == that.visitId &&
				shinryoucode == that.shinryoucode;
	}

	@Override
	public int hashCode() {

		return Objects.hash(shinryouId, visitId, shinryoucode);
	}

	@Override
	public String toString() {
		return "ShinryouDTO{" +
				"shinryouId=" + shinryouId +
				", visitId=" + visitId +
				", shinryoucode=" + shinryoucode +
				'}';
	}
}