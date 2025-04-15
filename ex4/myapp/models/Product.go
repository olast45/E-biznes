package models

type Product struct {
	ID    uint	`json:"id" gorm:"primaryKey"`
	Name  string	`json:"name" validate:"required"`
	Price float32	`json:"price" validate:"required"`
	CategoryID *uint      `json:"category_id"`
}
