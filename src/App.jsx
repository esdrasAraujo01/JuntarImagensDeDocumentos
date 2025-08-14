import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Upload, RotateCcw, Download, Combine, Crop, BookOpen, Zap, Smartphone, Globe, Loader2 } from 'lucide-react'
import { ImageUpload } from './components/ImageUpload.jsx'
import { ImageViewer } from './components/ImageViewer.jsx'
import { correctPerspective, combineImages, downloadImage } from './utils/imageProcessing.js'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('perspective')
  
  // Perspective correction state
  const [perspectiveImage, setPerspectiveImage] = useState(null)
  const [perspectivePoints, setPerspectivePoints] = useState([])
  const [correctedImage, setCorrectedImage] = useState(null)
  const [isProcessingPerspective, setIsProcessingPerspective] = useState(false)
  
  // Image combination state
  const [image1, setImage1] = useState(null)
  const [image2, setImage2] = useState(null)
  const [combinedImage, setCombinedImage] = useState(null)
  const [isProcessingCombination, setIsProcessingCombination] = useState(false)
  const [combineOptions, setCombineOptions] = useState({
    orientation: 'horizontal',
    alignment: 'center',
    overlap: 0
  })

  // Perspective correction handlers
  const handlePerspectiveImageLoad = (imageData) => {
    setPerspectiveImage(imageData)
    setPerspectivePoints([])
    setCorrectedImage(null)
  }

  const handlePointSelect = (point) => {
    if (perspectivePoints.length < 4) {
      setPerspectivePoints([...perspectivePoints, point])
    }
  }

  const handleResetPoints = () => {
    setPerspectivePoints([])
  }

  const handleCorrectPerspective = async () => {
    if (perspectivePoints.length === 4 && perspectiveImage) {
      setIsProcessingPerspective(true)
      try {
        const correctedImageUrl = await correctPerspective(perspectiveImage.url, perspectivePoints)
        setCorrectedImage(correctedImageUrl)
      } catch (error) {
        console.error('Error correcting perspective:', error)
        alert('Erro ao corrigir perspectiva: ' + error.message)
      } finally {
        setIsProcessingPerspective(false)
      }
    }
  }

  // Image combination handlers
  const handleImage1Load = (imageData) => {
    setImage1(imageData)
    setCombinedImage(null)
  }

  const handleImage2Load = (imageData) => {
    setImage2(imageData)
    setCombinedImage(null)
  }

  const handleCombineImages = async () => {
    if (image1 && image2) {
      setIsProcessingCombination(true)
      try {
        const combinedImageUrl = await combineImages(image1.url, image2.url, combineOptions)
        setCombinedImage(combinedImageUrl)
      } catch (error) {
        console.error('Error combining images:', error)
        alert('Erro ao combinar imagens: ' + error.message)
      } finally {
        setIsProcessingCombination(false)
      }
    }
  }

  const handleOptionChange = (option, value) => {
    setCombineOptions(prev => ({
      ...prev,
      [option]: value
    }))
  }

  // Download handlers
  const handleDownloadCorrected = () => {
    if (correctedImage) {
      downloadImage(correctedImage, 'perspectiva-corrigida.png')
    }
  }

  const handleDownloadCombined = () => {
    if (combinedImage) {
      downloadImage(combinedImage, 'imagens-combinadas.png')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <BookOpen className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Digitalização de Livros</h1>
              </div>
            </div>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              Versão Web
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Digitalize seus livros antigos com facilidade
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Uma interface moderna e unificada para corrigir perspectiva e combinar páginas de livros digitalizados.
            Simples, rápido e acessível em qualquer dispositivo.
          </p>
          
          {/* Benefits */}
            <div className="flex flex-col items-center p-4">
              <Zap className="h-12 w-12 text-green-600 mb-3" />
              <h3 className="font-semibold text-gray-900 mb-2">Rápido e Eficiente</h3>
              <p className="text-gray-600 text-sm">Processamento otimizado e interface intuitiva</p>
            </div>
        </div>

        {/* Main Tools */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="perspective" className="flex items-center space-x-2">
              <Crop className="h-4 w-4" />
              <span>Correção de Perspectiva</span>
            </TabsTrigger>
            <TabsTrigger value="combine" className="flex items-center space-x-2">
              <Combine className="h-4 w-4" />
              <span>Combinar Páginas</span>
            </TabsTrigger>
          </TabsList>

          {/* Perspective Correction Tab */}
          <TabsContent value="perspective">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Crop className="h-5 w-5" />
                  <span>Correção de Perspectiva</span>
                </CardTitle>
                <CardDescription>
                  Corrija distorções e ângulos em fotos de páginas de livros
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Upload and Controls */}
                  <div className="space-y-4">
                    <ImageUpload 
                      onImageLoad={handlePerspectiveImageLoad}
                      placeholder="Arraste e solte ou clique para selecionar a imagem da página"
                    />
                    
                    {/* Controls */}
                    <div className="space-y-3">
                      <Button 
                        variant="outline" 
                        className="w-full"
                        onClick={handleResetPoints}
                        disabled={perspectivePoints.length === 0}
                      >
                        <RotateCcw className="h-4 w-4 mr-2" />
                        Resetar Pontos ({perspectivePoints.length}/4)
                      </Button>
                      <Button 
                        className="w-full"
                        onClick={handleCorrectPerspective}
                        disabled={perspectivePoints.length !== 4 || !perspectiveImage || isProcessingPerspective}
                      >
                        {isProcessingPerspective ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            Processando...
                          </>
                        ) : (
                          'Corrigir Perspectiva'
                        )}
                      </Button>
                      <Button 
                        variant="outline" 
                        className="w-full"
                        disabled={!correctedImage}
                        onClick={handleDownloadCorrected}
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Baixar Resultado
                      </Button>
                    </div>
                  </div>

                  {/* Image Viewer */}
                  <div className="space-y-4">
                    <ImageViewer
                      imageUrl={perspectiveImage?.url}
                      points={perspectivePoints}
                      onPointSelect={handlePointSelect}
                      showPoints={true}
                      title="Imagem Original"
                    />
                  </div>
                </div>

                {/* Corrected Image Preview */}
                {correctedImage && (
                  <div className="mt-8">
                    <ImageViewer
                      imageUrl={correctedImage}
                      showPoints={false}
                      title="Imagem Corrigida"
                    />
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Combine Images Tab */}
          <TabsContent value="combine">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Combine className="h-5 w-5" />
                  <span>Combinar Páginas</span>
                </CardTitle>
                <CardDescription>
                  Junte duas páginas em uma única imagem
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
                  {/* Image 1 */}
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Página 1</h3>
                    <ImageUpload 
                      onImageLoad={handleImage1Load}
                      placeholder="Primeira página"
                    />
                  </div>

                  {/* Image 2 */}
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Página 2</h3>
                    <ImageUpload 
                      onImageLoad={handleImage2Load}
                      placeholder="Segunda página"
                    />
                  </div>

                  {/* Result Preview */}
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Resultado</h3>
                    <div className="border rounded-lg p-6 min-h-[200px] flex items-center justify-center bg-gray-50">
                      {combinedImage ? (
                        <img 
                          src={combinedImage} 
                          alt="Resultado combinado" 
                          className="max-w-full max-h-48 object-contain"
                        />
                      ) : (
                        <div className="text-center text-gray-500">
                          <Combine className="h-8 w-8 mx-auto mb-2 opacity-50" />
                          <p className="text-sm">Resultado aparecerá aqui</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Options */}
                <div className="p-6 bg-gray-50 rounded-lg">
                  <h4 className="font-medium text-gray-900 mb-4">Opções de Combinação</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Orientação
                      </label>
                      <div className="space-y-2">
                        <label className="flex items-center">
                          <input 
                            type="radio" 
                            name="orientation" 
                            value="horizontal" 
                            className="mr-2"
                            checked={combineOptions.orientation === 'horizontal'}
                            onChange={(e) => handleOptionChange('orientation', e.target.value)}
                          />
                          <span className="text-sm">Horizontal</span>
                        </label>
                        <label className="flex items-center">
                          <input 
                            type="radio" 
                            name="orientation" 
                            value="vertical" 
                            className="mr-2"
                            checked={combineOptions.orientation === 'vertical'}
                            onChange={(e) => handleOptionChange('orientation', e.target.value)}
                          />
                          <span className="text-sm">Vertical</span>
                        </label>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Alinhamento
                      </label>
                      <div className="space-y-2">
                        <label className="flex items-center">
                          <input 
                            type="radio" 
                            name="alignment" 
                            value="start" 
                            className="mr-2"
                            checked={combineOptions.alignment === 'start'}
                            onChange={(e) => handleOptionChange('alignment', e.target.value)}
                          />
                          <span className="text-sm">Início</span>
                        </label>
                        <label className="flex items-center">
                          <input 
                            type="radio" 
                            name="alignment" 
                            value="center" 
                            className="mr-2"
                            checked={combineOptions.alignment === 'center'}
                            onChange={(e) => handleOptionChange('alignment', e.target.value)}
                          />
                          <span className="text-sm">Centro</span>
                        </label>
                        <label className="flex items-center">
                          <input 
                            type="radio" 
                            name="alignment" 
                            value="end" 
                            className="mr-2"
                            checked={combineOptions.alignment === 'end'}
                            onChange={(e) => handleOptionChange('alignment', e.target.value)}
                          />
                          <span className="text-sm">Fim</span>
                        </label>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Sobreposição (px)
                      </label>
                      <input 
                        type="number" 
                        min="0" 
                        max="500" 
                        value={combineOptions.overlap}
                        onChange={(e) => handleOptionChange('overlap', parseInt(e.target.value) || 0)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>
                  
                  <div className="flex space-x-4">
                    <Button 
                      className="flex-1"
                      onClick={handleCombineImages}
                      disabled={!image1 || !image2 || isProcessingCombination}
                    >
                      {isProcessingCombination ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Combinando...
                        </>
                      ) : (
                        'Combinar Imagens'
                      )}
                    </Button>
                    <Button 
                      variant="outline" 
                      className="flex-1"
                      disabled={!combinedImage}
                      onClick={handleDownloadCombined}
                    >
                      <Download className="h-4 w-4 mr-2" />
                      Baixar Resultado
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>Digitalização de Livros</p>
            <p className="text-sm mt-2">Desenvolvido para facilitar a preservação digital de livros antigos</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

