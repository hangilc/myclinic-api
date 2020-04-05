package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

import java.util.Objects;

@MysqlTable("visit_drug")
public class DrugDTO {
	@Primary
	@AutoInc
	public int drugId;
	public int visitId;
	@MysqlColName("d_iyakuhincode")
	public int iyakuhincode;
	@MysqlColName("d_amount")
	public double amount;
	@MysqlColName("d_usage")
	public String usage;
	@MysqlColName("d_days")
	public int days;
	@MysqlColName("d_category")
	public int category;
	@MysqlColName("d_prescribed")
	public int prescribed;

	public static DrugDTO copy(DrugDTO src){
		DrugDTO dst = new DrugDTO();
		dst.drugId = src.drugId;
		dst.visitId = src.visitId;
		dst.iyakuhincode = src.iyakuhincode;
		dst.amount = src.amount;
		dst.usage = src.usage;
		dst.days = src.days;
		dst.category = src.category;
		dst.prescribed = src.prescribed;
		return dst;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		DrugDTO drugDTO = (DrugDTO) o;
		return drugId == drugDTO.drugId &&
				visitId == drugDTO.visitId &&
				iyakuhincode == drugDTO.iyakuhincode &&
				Double.compare(drugDTO.amount, amount) == 0 &&
				days == drugDTO.days &&
				category == drugDTO.category &&
				prescribed == drugDTO.prescribed &&
				Objects.equals(usage, drugDTO.usage);
	}

	@Override
	public int hashCode() {
		return Objects.hash(drugId, visitId, iyakuhincode, amount, usage, days, category, prescribed);
	}

	@Override
	public String toString() {
		return "DrugDTO{" +
				"drugId=" + drugId +
				", visitId=" + visitId +
				", iyakuhincode=" + iyakuhincode +
				", amount=" + amount +
				", usage='" + usage + '\'' +
				", days=" + days +
				", category=" + category +
				", prescribed=" + prescribed +
				'}';
	}
}