package dev.myclinic.dto;

public class DrugWithAttrDTO {

    public DrugDTO drug;
    public DrugAttrDTO attr;

    public static DrugWithAttrDTO create(DrugDTO drug, DrugAttrDTO attr){
        DrugWithAttrDTO result = new DrugWithAttrDTO();
        result.drug = drug;
        result.attr = attr;
        return result;
    }

    @Override
    public String toString() {
        return "DrugWithAttrDTO{" +
                "drug=" + drug +
                ", attr=" + attr +
                '}';
    }
}
