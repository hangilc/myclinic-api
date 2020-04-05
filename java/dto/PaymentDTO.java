package dev.myclinic.dto;

import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

@MysqlTable("visit_payment")
public class PaymentDTO {
	@Primary
	public int visitId;
	public int amount;
	@Primary
	@TypeHint({"datetime"})
	public String paytime;

	@Override
	public String toString() {
		return "PaymentDTO{" +
				"visitId=" + visitId +
				", amount=" + amount +
				", paytime='" + paytime + '\'' +
				'}';
	}
}