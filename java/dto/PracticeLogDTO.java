package dev.myclinic.dto;

@MysqlTable("practice_log")
public class PracticeLogDTO {

	@Primary
	@AutoInc
  	@MysqlColName("practice_log_id")
    public int serialId;
   	@TypeHint({"datetime"})
    public String createdAt;
    public String kind;
    public String body;

    public PracticeLogDTO(){}

    public PracticeLogDTO(int serialId, String createdAt, String kind, String body) {
        this.serialId = serialId;
        this.createdAt = createdAt;
        this.kind = kind;
        this.body = body;
    }

    @Override
    public String toString() {
        return "PracticeLogDTO{" +
                "serialId=" + serialId +
                ", createdAt='" + createdAt + '\'' +
                ", kind='" + kind + '\'' +
                ", body='" + body + '\'' +
                '}';
    }
}
