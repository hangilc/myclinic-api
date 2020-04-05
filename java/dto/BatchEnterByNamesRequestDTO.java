package dev.myclinic.dto;

import java.util.List;

public class BatchEnterByNamesRequestDTO {

    public List<String> shinryouNames;
    public List<EnterConductByNamesRequestDTO> conducts;

    @Override
    public String toString() {
        return "BatchEnterByNamesRequestDTO{" +
                "shinryouNames=" + shinryouNames +
                ", conducts=" + conducts +
                '}';
    }
}
