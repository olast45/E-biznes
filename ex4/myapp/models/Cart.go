package models

type Cart struct {
	ID    uint	`json:"id" gorm:"primaryKey"`
	Total  float32	`json:"total" validate:"required"`
}