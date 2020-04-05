package dev.myclinic.dto;

import java.util.List;

public class IntraclinicPostFullPageDTO {
    public int totalPages;
    public List<IntraclinicPostFullDTO> posts;

    @Override
    public String toString() {
        return "IntraclinicPostFullPageDTO{" +
                "totalPages=" + totalPages +
                ", posts=" + posts +
                '}';
    }
}
