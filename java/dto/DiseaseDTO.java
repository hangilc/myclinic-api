package dev.myclinic.dto;

import dev.myclinic.dto.annotation.AutoInc;
import dev.myclinic.dto.annotation.MysqlTable;
import dev.myclinic.dto.annotation.Primary;

import java.util.Objects;

@MysqlTable("disease")
public class DiseaseDTO {

    @Primary
    @AutoInc
    public int diseaseId;
    public int patientId;
    public int shoubyoumeicode;
    @TypeHint({"date"})
    public String startDate;
    @TypeHint({"date", "nullable"})
    public String endDate;
    public char endReason;

    public static DiseaseDTO copy(DiseaseDTO src){
        DiseaseDTO dst = new DiseaseDTO();
        dst.diseaseId = src.diseaseId;
        dst.patientId = src.patientId;
        dst.shoubyoumeicode = src.shoubyoumeicode;
        dst.startDate = src.startDate;
        dst.endDate = src.endDate;
        dst.endReason = src.endReason;
        return dst;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        DiseaseDTO that = (DiseaseDTO) o;
        return diseaseId == that.diseaseId &&
                patientId == that.patientId &&
                shoubyoumeicode == that.shoubyoumeicode &&
                endReason == that.endReason &&
                Objects.equals(startDate, that.startDate) &&
                Objects.equals(endDate, that.endDate);
    }

    @Override
    public int hashCode() {

        return Objects.hash(diseaseId, patientId, shoubyoumeicode, startDate, endDate, endReason);
    }

    @Override
    public String toString() {
        return "DiseaseDTO{" +
                "diseaseId=" + diseaseId +
                ", patientId=" + patientId +
                ", shoubyoumeicode=" + shoubyoumeicode +
                ", startDate='" + startDate + '\'' +
                ", endDate='" + endDate + '\'' +
                ", endReason=" + endReason +
                '}';
    }
}
