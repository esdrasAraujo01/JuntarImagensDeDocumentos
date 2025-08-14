import { useState, useRef, useEffect, useCallback } from 'react'
import { ZoomIn, ZoomOut, RotateCcw } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'

export function ImageViewer({ 
  imageUrl, 
  points = [], 
  onPointSelect, 
  showPoints = true,
  className = "",
  title = "Imagem"
}) {
  const canvasRef = useRef(null)
  const [scale, setScale] = useState(1)
  const [offset, setOffset] = useState({ x: 0, y: 0 })
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 })
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 })

  const drawCanvas = useCallback(() => {
    const canvas = canvasRef.current
    if (!canvas || !imageUrl) return

    const ctx = canvas.getContext('2d')
    const img = new Image()
    
    img.onload = () => {
      // Set canvas size
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
      
      // Calculate image dimensions to fit canvas
      const canvasAspect = canvas.width / canvas.height
      const imageAspect = img.width / img.height
      
      let drawWidth, drawHeight
      if (imageAspect > canvasAspect) {
        drawWidth = canvas.width
        drawHeight = canvas.width / imageAspect
      } else {
        drawHeight = canvas.height
        drawWidth = canvas.height * imageAspect
      }
      
      setImageSize({ width: drawWidth, height: drawHeight })
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // Apply transformations
      ctx.save()
      ctx.translate(canvas.width / 2 + offset.x, canvas.height / 2 + offset.y)
      ctx.scale(scale, scale)
      
      // Draw image centered
      ctx.drawImage(img, -drawWidth / 2, -drawHeight / 2, drawWidth, drawHeight)
      
      // Draw points if enabled
      if (showPoints && points.length > 0) {
        const colors = ['#ef4444', '#22c55e', '#3b82f6', '#eab308'] // red, green, blue, yellow
        
        points.forEach((point, index) => {
          if (point) {
            const x = (point.x - 0.5) * drawWidth
            const y = (point.y - 0.5) * drawHeight
            
            ctx.beginPath()
            ctx.arc(x, y, 8 / scale, 0, 2 * Math.PI)
            ctx.fillStyle = colors[index % colors.length]
            ctx.fill()
            ctx.strokeStyle = '#ffffff'
            ctx.lineWidth = 2 / scale
            ctx.stroke()
            
            // Draw number
            ctx.fillStyle = '#ffffff'
            ctx.font = `${12 / scale}px Arial`
            ctx.textAlign = 'center'
            ctx.fillText(index + 1, x, y + 4 / scale)
          }
        })
      }
      
      ctx.restore()
    }
    
    img.src = imageUrl
  }, [imageUrl, points, scale, offset, showPoints])

  useEffect(() => {
    drawCanvas()
  }, [drawCanvas])

  const handleCanvasClick = useCallback((e) => {
    if (!onPointSelect || !showPoints) return
    
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    
    // Get click coordinates relative to canvas
    const clickX = e.clientX - rect.left
    const clickY = e.clientY - rect.top
    
    // Convert to image coordinates (0-1 range)
    const centerX = canvas.width / 2 + offset.x
    const centerY = canvas.height / 2 + offset.y
    
    const imageX = (clickX - centerX) / scale / imageSize.width + 0.5
    const imageY = (clickY - centerY) / scale / imageSize.height + 0.5
    
    // Check if click is within image bounds
    if (imageX >= 0 && imageX <= 1 && imageY >= 0 && imageY <= 1) {
      onPointSelect({ x: imageX, y: imageY })
    }
  }, [onPointSelect, showPoints, scale, offset, imageSize])

  const handleMouseDown = useCallback((e) => {
    if (e.button === 0) { // Left mouse button
      setIsDragging(true)
      setDragStart({ x: e.clientX - offset.x, y: e.clientY - offset.y })
    }
  }, [offset])

  const handleMouseMove = useCallback((e) => {
    if (isDragging) {
      setOffset({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y
      })
    }
  }, [isDragging, dragStart])

  const handleMouseUp = useCallback(() => {
    setIsDragging(false)
  }, [])

  const handleZoomIn = useCallback(() => {
    setScale(prev => Math.min(prev * 1.2, 5))
  }, [])

  const handleZoomOut = useCallback(() => {
    setScale(prev => Math.max(prev / 1.2, 0.1))
  }, [])

  const handleReset = useCallback(() => {
    setScale(1)
    setOffset({ x: 0, y: 0 })
  }, [])

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-gray-900">{title}</h3>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" onClick={handleZoomIn}>
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={handleZoomOut}>
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={handleReset}>
            <RotateCcw className="h-4 w-4" />
          </Button>
        </div>
      </div>
      
      <div className="border rounded-lg overflow-hidden bg-gray-100">
        {imageUrl ? (
          <canvas
            ref={canvasRef}
            className="w-full h-96 cursor-crosshair"
            onClick={handleCanvasClick}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          />
        ) : (
          <div className="w-full h-96 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <div className="h-16 w-16 mx-auto mb-4 opacity-50">
                📷
              </div>
              <p>Nenhuma imagem carregada</p>
            </div>
          </div>
        )}
      </div>
      
      {showPoints && (
        <div className="text-sm text-gray-600">
          <p>Pontos selecionados: {points.filter(p => p).length}/4</p>
          {points.filter(p => p).length < 4 && (
            <p>Clique nos 4 cantos da página na ordem: superior esquerdo, superior direito, inferior direito, inferior esquerdo</p>
          )}
        </div>
      )}
    </div>
  )
}

