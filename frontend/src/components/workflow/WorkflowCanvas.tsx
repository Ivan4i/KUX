import { useCallback, useState, useEffect } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  NodeTypes,
  BackgroundVariant,
  Panel,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { RiSaveLine, RiPlayLine, RiDeleteBinLine, RiLoader4Line } from '@remixicon/react'
import toast from 'react-hot-toast'

import { TriggerNode } from './nodes/TriggerNode'
import { ActionNode } from './nodes/ActionNode'
import { ConditionNode } from './nodes/ConditionNode'
import { NodePalette } from './NodePalette'
import {
  getWorkflow,
  createWorkflow,
  updateWorkflow,
  runWorkflow,
  type WorkflowNode,
  type WorkflowEdge,
} from '@/services/api'

// Define node types
const nodeTypes: NodeTypes = {
  trigger: TriggerNode,
  action: ActionNode,
  condition: ConditionNode,
}

// Generate unique ID
const generateId = () => `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`

// Default empty canvas nodes for new workflow
const defaultNodes: Node[] = []
const defaultEdges: Edge[] = []

// Demo nodes for when no workflow is loaded
const demoNodes: Node[] = [
  {
    id: `trigger-${generateId()}`,
    type: 'trigger',
    position: { x: 250, y: 50 },
    data: {
      label: 'Загрузить из Notion',
      description: 'Получить ожидающие лиды',
      icon: 'notion',
    },
  },
  {
    id: `action-${generateId()}`,
    type: 'action',
    position: { x: 250, y: 180 },
    data: {
      label: 'Анализ через Gemini',
      description: 'Сгенерировать персональное сообщение',
      icon: 'gemini',
      agent: 'gemini',
    },
  },
  {
    id: `condition-${generateId()}`,
    type: 'condition',
    position: { x: 250, y: 320 },
    data: {
      label: 'Есть телефон?',
      description: 'Проверить наличие номера телефона',
      condition: 'lead.phone != null',
    },
  },
  {
    id: `action-wa-${generateId()}`,
    type: 'action',
    position: { x: 100, y: 460 },
    data: {
      label: 'Отправить WhatsApp',
      description: 'Отправить сообщение через WhatsApp',
      icon: 'whatsapp',
      agent: 'whatsapp',
    },
  },
  {
    id: `action-sms-${generateId()}`,
    type: 'action',
    position: { x: 400, y: 460 },
    data: {
      label: 'Отправить SMS',
      description: 'Отправить сообщение через SMS',
      icon: 'sms',
      agent: 'sms',
    },
  },
]

// Generate demo edges with connections
const createDemoEdges = (nodes: Node[]): Edge[] => {
  if (nodes.length < 5) return []
  return [
    {
      id: `edge-${generateId()}`,
      source: nodes[0].id,
      target: nodes[1].id,
      animated: true,
    },
    {
      id: `edge-${generateId()}`,
      source: nodes[1].id,
      target: nodes[2].id,
    },
    {
      id: `edge-${generateId()}`,
      source: nodes[2].id,
      target: nodes[3].id,
      sourceHandle: 'yes',
      label: 'Да',
      style: { stroke: '#10b981' },
    },
    {
      id: `edge-${generateId()}`,
      source: nodes[2].id,
      target: nodes[4].id,
      sourceHandle: 'no',
      label: 'Нет',
      style: { stroke: '#ef4444' },
    },
  ]
}

interface WorkflowCanvasProps {
  /** ID workflow для загрузки (редактирование существующего) */
  workflowId?: string
  /** Название нового workflow */
  workflowName?: string
  /** Описание нового workflow */
  workflowDescription?: string
  /** Показывать демо-узлы когда workflow не загружен */
  showDemo?: boolean
  /** Callback при сохранении */
  onSave?: (nodes: Node[], edges: Edge[]) => void
  /** Callback при запуске */
  onRun?: () => void
  /** Callback при создании/обновлении workflow */
  onWorkflowSaved?: (workflow: { id: string; name: string }) => void
}

export function WorkflowCanvas({
  workflowId,
  workflowName = 'Новый Workflow',
  workflowDescription,
  showDemo = true,
  onSave,
  onRun,
  onWorkflowSaved,
}: WorkflowCanvasProps) {
  // Create initial demo data once
  const [initialDemo] = useState(() => {
    const nodes = showDemo ? demoNodes : defaultNodes
    const edges = showDemo ? createDemoEdges(nodes) : defaultEdges
    return { nodes, edges }
  })

  const [currentWorkflowId, setCurrentWorkflowId] = useState<string | null>(workflowId || null)
  const [currentWorkflowName, setCurrentWorkflowName] = useState(workflowName)
  const [nodes, setNodes, onNodesChange] = useNodesState(initialDemo.nodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialDemo.edges)
  const [selectedNodes, setSelectedNodes] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [isRunning, setIsRunning] = useState(false)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)

  // Load workflow when workflowId changes
  useEffect(() => {
    if (workflowId) {
      loadWorkflow(workflowId)
    }
  }, [workflowId])

  // Track unsaved changes
  useEffect(() => {
    setHasUnsavedChanges(true)
  }, [nodes, edges])

  // Load existing workflow from API
  const loadWorkflow = async (id: string) => {
    try {
      setIsLoading(true)
      const workflow = await getWorkflow(id)

      // Convert API format to ReactFlow format
      const loadedNodes: Node[] = workflow.nodes.map((n: WorkflowNode) => ({
        id: n.id,
        type: n.type,
        position: n.position,
        data: n.data,
      }))

      const loadedEdges: Edge[] = workflow.edges.map((e: WorkflowEdge) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        sourceHandle: e.sourceHandle || undefined,
        targetHandle: e.targetHandle || undefined,
        label: e.label || undefined,
        animated: e.animated || false,
        style: e.style || undefined,
      }))

      setNodes(loadedNodes)
      setEdges(loadedEdges)
      setCurrentWorkflowId(workflow.id)
      setCurrentWorkflowName(workflow.name)
      setHasUnsavedChanges(false)

      toast.success(`Загружен workflow: ${workflow.name}`)
    } catch (error) {
      console.error('Ошибка загрузки workflow:', error)
      toast.error('Не удалось загрузить workflow')
    } finally {
      setIsLoading(false)
    }
  }

  // Handle new connections
  const onConnect = useCallback(
    (params: Connection) => {
      const newEdge = {
        ...params,
        id: `edge-${generateId()}`,
        animated: true,
      }
      setEdges((eds) => addEdge(newEdge, eds))
    },
    [setEdges]
  )

  // Handle node selection
  const onSelectionChange = useCallback(
    ({ nodes: selectedNodes }: { nodes: Node[] }) => {
      setSelectedNodes(selectedNodes.map((n) => n.id))
    },
    []
  )

  // Handle drop from palette
  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault()

      const type = event.dataTransfer.getData('application/reactflow')
      const nodeDataStr = event.dataTransfer.getData('application/nodedata')

      if (!type || !nodeDataStr) return

      const nodeData = JSON.parse(nodeDataStr)

      const position = {
        x: event.clientX - 250,
        y: event.clientY - 100,
      }

      const newNode: Node = {
        id: `${type}-${generateId()}`,
        type,
        position,
        data: nodeData,
      }

      setNodes((nds) => [...nds, newNode])
    },
    [setNodes]
  )

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  // Delete selected nodes
  const deleteSelected = useCallback(() => {
    setNodes((nds) => nds.filter((n) => !selectedNodes.includes(n.id)))
    setEdges((eds) => eds.filter((e) =>
      !selectedNodes.includes(e.source) && !selectedNodes.includes(e.target)
    ))
    setSelectedNodes([])
  }, [selectedNodes, setNodes, setEdges])

  // Save workflow to API
  const handleSave = useCallback(async () => {
    try {
      setIsSaving(true)

      // Convert ReactFlow format to API format
      // For NEW workflows, regenerate IDs to ensure uniqueness
      const isNew = !currentWorkflowId
      const idPrefix = isNew ? generateId() : ''

      const apiNodes: WorkflowNode[] = nodes.map((n) => ({
        id: isNew ? `${idPrefix}-${n.id}` : n.id,
        type: n.type || 'action',
        position: n.position,
        data: n.data || {},
      }))

      // Create a mapping of old to new IDs for edges
      const nodeIdMap: Record<string, string> = {}
      nodes.forEach((n, i) => {
        nodeIdMap[n.id] = apiNodes[i].id
      })

      const apiEdges: WorkflowEdge[] = edges.map((e) => ({
        id: isNew ? `${idPrefix}-${e.id}` : e.id,
        source: isNew ? nodeIdMap[e.source] || e.source : e.source,
        target: isNew ? nodeIdMap[e.target] || e.target : e.target,
        sourceHandle: e.sourceHandle || null,
        targetHandle: e.targetHandle || null,
        label: typeof e.label === 'string' ? e.label : null,
        animated: e.animated || false,
        style: e.style || null,
      }))

      let savedWorkflow

      if (currentWorkflowId) {
        // Update existing workflow
        savedWorkflow = await updateWorkflow(currentWorkflowId, {
          nodes: apiNodes,
          edges: apiEdges,
        })
        toast.success('Workflow сохранён!')
      } else {
        // Create new workflow
        savedWorkflow = await createWorkflow({
          name: currentWorkflowName,
          description: workflowDescription,
          nodes: apiNodes,
          edges: apiEdges,
        })
        setCurrentWorkflowId(savedWorkflow.id)

        // Update local IDs to match saved ones
        setNodes(savedWorkflow.nodes.map((n: WorkflowNode) => ({
          id: n.id,
          type: n.type,
          position: n.position,
          data: n.data,
        })))
        setEdges(savedWorkflow.edges.map((e: WorkflowEdge) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          sourceHandle: e.sourceHandle || undefined,
          targetHandle: e.targetHandle || undefined,
          label: e.label || undefined,
          animated: e.animated || false,
          style: e.style || undefined,
        })))

        toast.success('Workflow создан!')
      }

      setHasUnsavedChanges(false)

      // Call callbacks
      if (onSave) {
        onSave(nodes, edges)
      }
      if (onWorkflowSaved && savedWorkflow) {
        onWorkflowSaved({ id: savedWorkflow.id, name: savedWorkflow.name })
      }
    } catch (error) {
      console.error('Ошибка сохранения workflow:', error)
      toast.error('Не удалось сохранить workflow')
    } finally {
      setIsSaving(false)
    }
  }, [nodes, edges, currentWorkflowId, currentWorkflowName, workflowDescription, onSave, onWorkflowSaved, setNodes, setEdges])

  // Run workflow
  const handleRun = useCallback(async () => {
    // Save first if there are unsaved changes
    if (hasUnsavedChanges || !currentWorkflowId) {
      await handleSave()
    }

    if (!currentWorkflowId) {
      toast.error('Сначала сохраните workflow')
      return
    }

    try {
      setIsRunning(true)
      await runWorkflow(currentWorkflowId)
      toast.success('Workflow запущен!')

      if (onRun) {
        onRun()
      }
    } catch (error) {
      console.error('Ошибка запуска workflow:', error)
      toast.error('Не удалось запустить workflow')
    } finally {
      setIsRunning(false)
    }
  }, [currentWorkflowId, hasUnsavedChanges, handleSave, onRun])

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-200px)] bg-gray-50 rounded-lg border border-gray-200 items-center justify-center">
        <div className="flex items-center gap-2 text-gray-500">
          <RiLoader4Line className="size-5 animate-spin" />
          Загрузка workflow...
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-[calc(100vh-200px)] bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
      {/* Палитра узлов */}
      <NodePalette />

      {/* Холст */}
      <div className="flex-1" onDrop={onDrop} onDragOver={onDragOver}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onSelectionChange={onSelectionChange}
          nodeTypes={nodeTypes}
          fitView
          snapToGrid
          snapGrid={[15, 15]}
          defaultEdgeOptions={{
            style: { strokeWidth: 2, stroke: '#94a3b8' },
            type: 'smoothstep',
          }}
        >
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              switch (node.type) {
                case 'trigger': return '#8b5cf6'
                case 'action': return '#3b82f6'
                case 'condition': return '#f59e0b'
                default: return '#94a3b8'
              }
            }}
            maskColor="rgba(0, 0, 0, 0.1)"
          />
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} />

          {/* Панель действий */}
          <Panel position="top-right" className="flex gap-2">
            {selectedNodes.length > 0 && (
              <button
                onClick={deleteSelected}
                className="flex items-center gap-2 px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
              >
                <RiDeleteBinLine className="size-4" />
                Удалить ({selectedNodes.length})
              </button>
            )}
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="flex items-center gap-2 px-3 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm disabled:opacity-50"
            >
              {isSaving ? (
                <RiLoader4Line className="size-4 animate-spin" />
              ) : (
                <RiSaveLine className="size-4" />
              )}
              {hasUnsavedChanges ? 'Сохранить*' : 'Сохранить'}
            </button>
            <button
              onClick={handleRun}
              disabled={isRunning || nodes.length === 0}
              className="flex items-center gap-2 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm disabled:opacity-50"
            >
              {isRunning ? (
                <RiLoader4Line className="size-4 animate-spin" />
              ) : (
                <RiPlayLine className="size-4" />
              )}
              Запустить
            </button>
          </Panel>

          {/* Информационная панель */}
          <Panel position="top-left" className="bg-white/90 backdrop-blur-sm rounded-lg px-3 py-2 shadow-sm border border-gray-200">
            <div className="text-sm font-medium text-gray-900">{currentWorkflowName}</div>
            <div className="text-xs text-gray-500">
              {nodes.length} узлов, {edges.length} связей
              {currentWorkflowId && <span className="ml-2 text-green-600">(сохранено)</span>}
              {!currentWorkflowId && <span className="ml-2 text-amber-600">(не сохранено)</span>}
            </div>
          </Panel>
        </ReactFlow>
      </div>
    </div>
  )
}
