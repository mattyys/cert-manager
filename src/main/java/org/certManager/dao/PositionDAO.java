package org.certManager.dao;

import java.util.List;
import java.util.Optional;

import org.certManager.model.Position;

public interface PositionDAO {
    
    Position createPosition(String positionName);
    Optional<Position> getPositionById(int id);
    Optional<Position> getPositionByName(String positionName);
    List<Position> getAllPositions();
    void updatePosition(Position position);
    
    void deletePosition(int id);
    

}
