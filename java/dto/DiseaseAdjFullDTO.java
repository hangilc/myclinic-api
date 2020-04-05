package dev.myclinic.dto;

public class DiseaseAdjFullDTO {
    public DiseaseAdjDTO diseaseAdj;
    public ShuushokugoMasterDTO master;

    @Override
    public String toString() {
        return "DiseaseAdjFullDTO{" +
                "diseaseAdj=" + diseaseAdj +
                ", master=" + master +
                '}';
    }

    public static DiseaseAdjFullDTO create(DiseaseAdjDTO adj, ShuushokugoMasterDTO master){
        DiseaseAdjFullDTO result = new DiseaseAdjFullDTO();
        result.diseaseAdj = adj;
        result.master = master;
        return result;
    }
}
