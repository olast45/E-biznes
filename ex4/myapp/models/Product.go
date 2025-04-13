package models

type Product struct {
	ID    uint	`json:"id" gorm:"primaryKey"`
	Name  string	`json:"name"`
	Price float32	`json:"price"`
}
