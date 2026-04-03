from sqlalchemy.orm import Session
from precognito.work_orders.database import SessionLocal
from precognito.work_orders import models
import logging

logger = logging.getLogger(__name__)

def create_automatic_work_order(device_id: str, severity: str, reason: str):
    """
    US-4.1: Automatically generate a work order when anomaly exceeds threshold.
    """
    db = SessionLocal()
    try:
        # Check if there's already an active work order for this device to avoid duplicates
        existing = db.query(models.Audit).filter(
            models.Audit.assetId == device_id,
            models.Audit.status.in_(["PENDING", "IN_PROGRESS", "CHECK_IN"])
        ).first()
        
        if existing:
            logger.info(f"Active work order already exists for {device_id}, skipping auto-generation.")
            return None
            
        new_wo = models.Audit(
            assetId=device_id,
            status="PENDING",
            remarks=f"AUTO-GENERATED: {severity} anomaly detected. Reason: {reason}"
        )
        db.add(new_wo)
        db.commit()
        db.refresh(new_wo)
        
        logger.info(f"✅ Automatically created Work Order {new_wo.id} for {device_id}")
        return new_wo
    except Exception as e:
        logger.error(f"Failed to auto-generate work order: {e}")
        db.rollback()
    finally:
        db.close()
