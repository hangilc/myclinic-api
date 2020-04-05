package dev.myclinic.dto;

import java.util.List;

public class VisitDrugDTO {

    public VisitDTO visit;
    public List<DrugFullDTO> drugs;

    @Override
    public String toString() {
        return "VisitDrugDTO{" +
                "visit=" + visit +
                ", drugs=" + drugs +
                '}';
    }
}
