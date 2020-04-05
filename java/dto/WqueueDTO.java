package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

import java.util.Objects;

@MysqlTable("wqueue")
public class WqueueDTO {
	@Primary
	public int visitId;
	public int waitState;

	public static WqueueDTO copy(WqueueDTO src){
		WqueueDTO dst = new WqueueDTO();
		dst.visitId = src.visitId;
		dst.waitState = src.waitState;
		return dst;
	}

	@Override
	public String toString() {
		return "WqueueDTO{" +
				"visitId=" + visitId +
				", waitState=" + waitState +
				'}';
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		WqueueDTO wqueueDTO = (WqueueDTO) o;
		return visitId == wqueueDTO.visitId &&
				waitState == wqueueDTO.waitState;
	}

	@Override
	public int hashCode() {

		return Objects.hash(visitId, waitState);
	}
}